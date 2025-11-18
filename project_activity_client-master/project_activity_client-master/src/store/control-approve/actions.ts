import type {
	IApproveUser,
	IApproveUserRequest,
	IRejectUserRequest,
} from './types';

import { createAsyncThunk } from '@reduxjs/toolkit';
import {
	getApproveUsers,
	approveUser,
	rejectUser,
} from '../../shared/api/control';

export const getApproveUsersAction = createAsyncThunk<IApproveUser[]>(
	'controlApprove/getApproveUsers',
	getApproveUsers
);

export const approveUserAction = createAsyncThunk<
	IApproveUser,
	IApproveUserRequest
>('controlApprove/approveUser', approveUser);

export const rejectUserAction = createAsyncThunk<
	IApproveUser,
	IRejectUserRequest
>('controlApprove/rejectUser', rejectUser);
