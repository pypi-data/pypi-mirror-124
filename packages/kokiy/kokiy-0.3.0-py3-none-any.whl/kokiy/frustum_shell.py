import numpy as np
from scipy.spatial.transform import Rotation as R

from kokiy.shell_2d import Shell2D
from kokiy.axishell import _compute_shell_crest
from kokiy.axishell import _compute_shellcrest_nml


class FrustumShell(Shell2D):
    geom_type = 'frustum'

    def __init__(self, n_azi, n_longi, pt_left, pt_right, radius_left,
                 radius_right, direc_point=None):
        super().__init__(n_azi, n_longi)

        self.pt_left = np.array(pt_left)
        self.pt_right = np.array(pt_right)
        self.radius_left = radius_left
        self.radius_right = radius_right

        # useful vars
        self._direc = self.pt_right - self.pt_left  # normal direction
        self._direc_unit = self._direc / np.linalg.norm(self._direc)
        self._ort_direc = np.array(direc_point) / np.linal.norm(direc_point) if direc_point is not None else self._find_orthogonal_direc()

        self._build_shell()

    def _find_orthogonal_direc(self):
        # find an orthogonal direction
        delta_vec = self._direc_unit + np.array([1., 2., 3.])  # avoid collinearity
        dist = np.dot(delta_vec, self._direc_unit)
        proj_point = (self.pt_right + delta_vec) - dist * self._direc_unit
        ort_direc = (proj_point - self.pt_right) / np.linalg.norm(proj_point - self.pt_right)
        return ort_direc / np.linalg.norm(ort_direc)

    def _build_shell(self):

        # Construct Shell Crest
        ctrl_pts_r = np.array([self._get_radius(v) for v in self.v[0]])
        shell_crest = _compute_shell_crest(self.v[0], ctrl_pts_r, self.shape[1])

        # Compute radius and theta matrices of shape (n_azi, n_longi)
        min_theta, max_theta = 0., np.deg2rad(360)
        theta_vec = np.linspace(min_theta, max_theta, num=self.shape[0])
        self.rad, self.theta = np.meshgrid(shell_crest[1], theta_vec)

        # Compute xyz matrix of shape (n_azi, n_longi, 3)
        # define rotations and auxiliar normals
        center_vec = np.array([self._direc_unit * v for v in self.v[0]])
        rotations = [R.from_rotvec(theta * self._direc_unit) for theta in theta_vec]
        aux_normals = self._get_aux_normals(rotations)

        # get xyz
        xyz = []
        for i, sect_center in enumerate(center_vec):
            sect_radius = self.rad[:, i][0]
            xyz.append(sect_center + sect_radius * aux_normals)

        self.x, self.y, self.z = [np.take(np.array(xyz), i, -1).T for i in range(3)]
        normals = [self._get_normals(aux_normals) for _ in range(self.shape[1])]
        self.n_x, self.n_y, self.n_z = [np.take(np.array(normals), i, -1).T for i in range(3)]
        shell_crest_scaled = shell_crest.copy()
        shell_crest_scaled[0] *= np.linalg.norm(self._direc)
        xr_nml_1d = _compute_shellcrest_nml(shell_crest)
        self.n_r = np.tile(xr_nml_1d[1], (self.shape[0], 1))

        # Compute du, dv matrix of shape (n_azi, n_longi)
        longi_vals = np.tile(shell_crest_scaled[0], (self.shape[0], 1))
        self.du = np.pad(np.sqrt(np.diff(longi_vals, axis=1) ** 2
                                 + np.diff(self.rad, axis=1) ** 2),
                         ((0, 0), (1, 0)), 'edge')
        self.dv = self.rad * np.pad(np.diff(self.theta, axis=0),
                                    ((1, 0), (0, 0)), 'edge')

        # Compute abs_curv array of shape (n_longi,)
        self.abs_curv = self._compute_abs_curv(self.du)

        # Compute weight intervals in u and v directions array of shape (n_transvers, n_longi)
        self.dwu, self.dwv = self._compute_weight_interv_adim(self.du, self.dv)

        # Compute surface nodes array of shape (n_transvers, n_longi)
        self.surf = self._compute_surf(self.dwu, self.dwv)

    def _get_radius(self, v):
        return (self.radius_right - self.radius_left) * v + self.radius_left

    def _get_aux_normals(self, rotations):
        return np.array([rotation.apply(self._ort_direc) for rotation in rotations])

    def _get_normals(self, aux_normals):
        dist_rad = self.radius_right - self.radius_left
        theta = np.arctan2(dist_rad, np.linalg.norm(self._direc))
        rotations = [R.from_rotvec(theta * np.cross(self._direc_unit, aux_normal)) for aux_normal in aux_normals]

        return np.array([rotation.apply(aux_norm) for rotation, aux_norm in zip(rotations, aux_normals)])

    def replicate(self, shape):
        return FrustumShell(*shape, self.pt_left, self.pt_right, self.radius_left,
                            self.radius_right)
