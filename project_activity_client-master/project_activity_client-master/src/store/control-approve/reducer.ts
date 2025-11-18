import type { IControlApproveStore, IApproveUser } from './types';

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

import * as actions from './actions';

const initialState: IControlApproveStore = {
	approveUsers: [],
	currentApproveUser: null,
	isOpenApproveModal: false,
	isOpenRejectModal: false,
	isOpenDetailModal: false,
	isLoadingApprove: false,
	isLoadingRequest: false,
	error: null,
};

export const controlApproveSlice = createSlice({
	name: 'controlApprove',
	initialState,
	reducers: {
		setCurrentApproveUser(state, action: PayloadAction<IApproveUser>) {
			state.currentApproveUser = action.payload;
		},
		clearCurrentApproveUser(state) {
			state.currentApproveUser = null;
		},
		openApproveModal(state) {
			state.isOpenApproveModal = true;
		},
		openRejectModal(state) {
			state.isOpenRejectModal = true;
		},
		openDetailModal(state) {
			state.isOpenDetailModal = true;
		},
		closeModals(state) {
			state.isOpenApproveModal = false;
			state.isOpenRejectModal = false;
			state.isOpenDetailModal = false;
		},
	},
	extraReducers: (builder) => {
		builder
			.addCase(actions.getApproveUsersAction.pending, (state) => {
				state.isLoadingApprove = true;
				state.error = null;
			})
			.addCase(actions.getApproveUsersAction.fulfilled, (state, action) => {
				state.isLoadingApprove = false;
				state.approveUsers = action.payload;
			})
			.addCase(actions.getApproveUsersAction.rejected, (state, action) => {
				state.isLoadingApprove = false;
				state.error =
					action.error?.message || 'Не удалось загрузить пользователей';
			})
			.addCase(actions.approveUserAction.pending, (state) => {
				state.isLoadingRequest = true;
				state.error = null;
			})
			.addCase(actions.approveUserAction.fulfilled, (state, action) => {
				const updatedUser = action.payload;
				state.approveUsers = state.approveUsers.map((user) =>
					user.id === updatedUser.id ? updatedUser : user
				);
				state.isLoadingRequest = false;
				state.currentApproveUser = null;
				state.isOpenApproveModal = false;
			})
			.addCase(actions.approveUserAction.rejected, (state, action) => {
				state.isLoadingRequest = false;
				state.error =
					action.error?.message || 'Не удалось загрузить пользователей';
			})
			.addCase(actions.rejectUserAction.pending, (state) => {
				state.isLoadingRequest = true;
				state.error = null;
			})
			.addCase(actions.rejectUserAction.fulfilled, (state, action) => {
				const updatedUser = action.payload;
				state.approveUsers = state.approveUsers.map((user) =>
					user.id === updatedUser.id ? updatedUser : user
				);
				state.isLoadingRequest = false;
				state.currentApproveUser = null;
				state.isOpenRejectModal = false;
			})
			.addCase(actions.rejectUserAction.rejected, (state, action) => {
				state.isLoadingRequest = false;
				state.error =
					action.error?.message || 'Не удалось загрузить пользователей';
			});
	},
});

export const {
	setCurrentApproveUser,
	clearCurrentApproveUser,
	openApproveModal,
	openRejectModal,
	openDetailModal,
	closeModals,
} = controlApproveSlice.actions;
