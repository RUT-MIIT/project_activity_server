import type { IField, IApplicationComment } from '../application/types';
import type { ICoordinationStore } from './types';

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

import * as actions from './actions';

const initialState: ICoordinationStore = {
	applications: [],
	application: null,
	applicationDetail: null,
	currentField: null,
	isLoadingApps: false,
	isLoadingDetail: false,
	isLoadingComment: false,
	error: null,
};

export const coordinationSlice = createSlice({
	name: 'coordination',
	initialState,
	reducers: {
		setCurrentField(state, action: PayloadAction<IField | null>) {
			state.currentField = action.payload;
		},
	},
	extraReducers: (builder) => {
		builder
			.addCase(actions.getCoordinationAppsAction.pending, (state) => {
				state.isLoadingApps = true;
				state.error = null;
			})
			.addCase(actions.getCoordinationAppsAction.fulfilled, (state, action) => {
				state.isLoadingApps = false;
				state.applications = action.payload;
			})
			.addCase(actions.getCoordinationAppsAction.rejected, (state, action) => {
				state.isLoadingApps = false;
				state.error = action.error?.message || 'Не удалось загрузить заявки';
			})
			.addCase(actions.getCoordinationAppDetailAction.pending, (state) => {
				state.isLoadingDetail = true;
				state.error = null;
			})
			.addCase(
				actions.getCoordinationAppDetailAction.fulfilled,
				(state, action) => {
					state.isLoadingDetail = false;
					state.applicationDetail = action.payload;
				}
			)
			.addCase(
				actions.getCoordinationAppDetailAction.rejected,
				(state, action) => {
					state.isLoadingDetail = false;
					state.error = action.error?.message || 'Не удалось загрузить заявку';
				}
			)
			.addCase(actions.createCommentToFieldAction.pending, (state) => {
				state.isLoadingComment = true;
				state.error = null;
			})
			.addCase(
				actions.createCommentToFieldAction.fulfilled,
				(state, action: PayloadAction<IApplicationComment>) => {
					state.isLoadingComment = false;
					if (state.applicationDetail) {
						state.applicationDetail.comments = [
							action.payload,
							...state.applicationDetail.comments,
						];
					}
				}
			)
			.addCase(actions.createCommentToFieldAction.rejected, (state, action) => {
				state.isLoadingComment = false;
				state.error = action.error?.message || 'Не удалось создать комментарий';
			});
	},
});

export const { setCurrentField } = coordinationSlice.actions;
