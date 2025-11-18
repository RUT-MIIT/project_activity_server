import type { IApplicationStore } from './types';

import { createSlice } from '@reduxjs/toolkit';

import * as actions from './actions';

const initialState: IApplicationStore = {
	applications: [],
	application: null,
	isLoading: false,
	error: null,
};

export const applicationSlice = createSlice({
	name: 'application',
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addCase(actions.getAppsAction.pending, (state) => {
				state.isLoading = true;
				state.error = null;
			})
			.addCase(actions.getAppsAction.fulfilled, (state, action) => {
				state.isLoading = false;
				state.applications = action.payload;
			})
			.addCase(actions.getAppsAction.rejected, (state, action) => {
				state.isLoading = false;
				state.error = action.error?.message || 'Не удалось загрузить заявки';
			})
			.addCase(actions.createAppMainAction.pending, (state) => {
				state.isLoading = true;
				state.error = null;
			})
			.addCase(actions.createAppMainAction.fulfilled, (state) => {
				state.isLoading = false;
			})
			.addCase(actions.createAppMainAction.rejected, (state, action) => {
				state.isLoading = false;
				state.error = action.error?.message || 'Произошла ошибка';
			})
			.addCase(actions.createAppPublicAction.pending, (state) => {
				state.isLoading = true;
				state.error = null;
			})
			.addCase(actions.createAppPublicAction.fulfilled, (state) => {
				state.isLoading = false;
			})
			.addCase(actions.createAppPublicAction.rejected, (state, action) => {
				state.isLoading = false;
				state.error = action.error?.message || 'Произошла ошибка';
			});
	},
});
