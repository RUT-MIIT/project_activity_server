import type { ICatalogStore } from './types';

import { createSlice } from '@reduxjs/toolkit';

import * as actions from './actions';

const initialState: ICatalogStore = {
	institutes: [],
	departments: [],
	roles: [],
	isLoadingCatalog: false,
	error: null,
};

export const catalogSlice = createSlice({
	name: 'catalog',
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addCase(actions.getInstitutesAction.pending, (state) => {
				state.isLoadingCatalog = true;
				state.error = null;
			})
			.addCase(actions.getInstitutesAction.fulfilled, (state, action) => {
				state.isLoadingCatalog = false;
				state.institutes = action.payload;
			})
			.addCase(actions.getInstitutesAction.rejected, (state, action) => {
				state.isLoadingCatalog = false;
				state.error = action.error?.message || 'Не удалось загрузить каталог';
			})
			.addCase(actions.getDepartmentsAction.pending, (state) => {
				state.isLoadingCatalog = true;
				state.error = null;
			})
			.addCase(actions.getDepartmentsAction.fulfilled, (state, action) => {
				state.isLoadingCatalog = false;
				state.departments = action.payload;
			})
			.addCase(actions.getDepartmentsAction.rejected, (state, action) => {
				state.isLoadingCatalog = false;
				state.error = action.error?.message || 'Не удалось загрузить каталог';
			})
			.addCase(actions.getRolesAction.pending, (state) => {
				state.isLoadingCatalog = true;
				state.error = null;
			})
			.addCase(actions.getRolesAction.fulfilled, (state, action) => {
				state.isLoadingCatalog = false;
				state.roles = action.payload;
			})
			.addCase(actions.getRolesAction.rejected, (state, action) => {
				state.isLoadingCatalog = false;
				state.error = action.error?.message || 'Не удалось загрузить каталог';
			});
	},
});
