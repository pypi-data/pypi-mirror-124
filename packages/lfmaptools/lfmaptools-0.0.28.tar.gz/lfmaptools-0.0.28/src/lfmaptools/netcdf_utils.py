import netCDF4 as nc
import numpy as np


def nc2np(filename, var=None):

    with nc.Dataset(filename, 'r') as rgrp:

        attrs = rgrp.__dict__

        tiles = list(rgrp.groups)
        nc_variables = list(rgrp[tiles[0]].variables)

        if var is not None:
            if var not in nc_variables:
                raise ValueError('variable {} not in netcdf file {}'.format(var, filename))

        nX = attrs['nXpertile']
        nY = attrs['nYpertile']
        nXY = nX*nY
        nrows = len(tiles)*nXY

        if var is None:
            variables = nc_variables.copy()
        else:
            variables = ['x_distance', 'y_distance', var]

        dt = [('tile',int)]
        for v in variables:
            if v=='x':
                vname = 'x_distance'
            elif v=='y':
                vname = 'y_distance'
            else:
                vname = v
            dt.append((vname, rgrp[tiles[0]][v].dtype))

        data = np.empty((nrows,), dtype=dt)
        
        #data[:] = np.nan

        if 'x' in variables:
            variables.remove('x')
        if 'y' in variables:
            variables.remove('y')

        if 'x_distance' in variables:
            variables.remove('x_distance')
        if 'y_distance' in variables:
            variables.remove('y_distance')

        for i, t in enumerate(tiles):
            grp = rgrp[t]
            if 'x' in nc_variables:
                x = grp['x'][:]
            elif 'x_distance' in nc_variables:
                x = grp['x_distance'][:]
            if 'y' in nc_variables:
                y = grp['y'][:]
            elif 'y_distance' in nc_variables:
                y = grp['y_distance'][:]
            Y, X = np.meshgrid(y,x)
            data['tile'][i*nXY:(i+1)*nXY] = int(t)
            data['x_distance'][i*nXY:(i+1)*nXY] = X.flatten()
            data['y_distance'][i*nXY:(i+1)*nXY] = Y.flatten()
            for v in variables:
                data[v][i*nXY:(i+1)*nXY] = grp[v][:].flatten()

    return data

def nc_max(filename, var=None):

    with nc.Dataset(filename, 'r') as rgrp:

        tiles = list(rgrp.groups)

        nc_variables = list(rgrp[tiles[0]].variables)

        if var is None:
            variables = nc_variables.copy()
        else:
            if isinstance(var, list):
                variables = [v for v in var if v in nc_variables]
            else:
                if var in nc_variables:
                    variables = [var] 
                else:
                    raise ValueError('variable {} not in netcdf file {}'.format(var, filename))
        max_vals = dict.fromkeys(variables, -np.inf)

        for t in tiles:
            grp = rgrp[t]
            for v in variables:
                max_vals[v] = max(max_vals[v], np.amax(grp[v][:]))

    return max_vals

def nc_min(filename, var=None):

    with nc.Dataset(filename, 'r') as rgrp:

        tiles = list(rgrp.groups)

        nc_variables = list(rgrp[tiles[0]].variables)

        if var is None:
            variables = nc_variables.copy()
        else:
            if isinstance(var, list):
                variables = [v for v in var if v in nc_variables]
            else:
                if var in nc_variables:
                    variables = [var] 
                else:
                    raise ValueError('variable {} not in netcdf file {}'.format(var, filename))
        min_vals = dict.fromkeys(variables, np.inf)

        for t in tiles:
            grp = rgrp[t]
            for v in variables:
                min_vals[v] = min(min_vals[v], np.amin(grp[v][:]))

    return min_vals