import type { IInstitute, IDepartment, IRole } from './types';

import { createAsyncThunk } from '@reduxjs/toolkit';
import {
	getInstitutesCatalog,
	getDepartmentsCatalog,
	getRolesCatalog,
} from '../../shared/api/catalog';

export const getInstitutesAction = createAsyncThunk<IInstitute[]>(
	'catalog/getInstitutes',
	getInstitutesCatalog
);

export const getDepartmentsAction = createAsyncThunk<IDepartment[]>(
	'catalog/getDepartments',
	getDepartmentsCatalog
);

export const getRolesAction = createAsyncThunk<IRole[]>(
	'catalog/getRoles',
	getRolesCatalog
);
