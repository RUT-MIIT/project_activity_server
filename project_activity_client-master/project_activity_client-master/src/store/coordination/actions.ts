import type {
	IApplicationItem,
	IApplicationDetail,
	IApplicationComment,
	IEditApp,
} from '../application/types';
import type { ICreateCommentAction, IAppActionResponse } from './types';

import { createAsyncThunk } from '@reduxjs/toolkit';
import {
	getCoordinationApps,
	getCoordinationDetail,
	createCommentToField,
	editApp,
	approveApp,
	reworkApp,
	rejectApp,
} from '../../shared/api/coordination';

export const getCoordinationAppsAction = createAsyncThunk<IApplicationItem[]>(
	'coordination/getApps',
	getCoordinationApps
);

export const getCoordinationAppDetailAction = createAsyncThunk<
	IApplicationDetail,
	string
>('coordination/getAppDetail', getCoordinationDetail);

export const createCommentToFieldAction = createAsyncThunk<
	IApplicationComment,
	ICreateCommentAction
>('coordination/createCommentToFiled', createCommentToField);

export const editAppAction = createAsyncThunk<
	IApplicationDetail,
	{ id: number; data: IEditApp }
>('coordination/editApp', async ({ id, data }) => {
	return editApp(id, data);
});

export const approveAppAction = createAsyncThunk<
	IAppActionResponse,
	{ applicationId: number }
>('coordination/approveApp', async ({ applicationId }) => {
	return approveApp(applicationId);
});

export const reworkAppAction = createAsyncThunk<
	IAppActionResponse,
	{ applicationId: number }
>('coordination/reworkApp', async ({ applicationId }) => {
	return reworkApp(applicationId);
});

export const rejectAppAction = createAsyncThunk<
	IAppActionResponse,
	{ applicationId: number; reason: string }
>('coordination/rejectApp', async ({ applicationId, reason }) => {
	return rejectApp(applicationId, reason);
});
