import type { IUserStore } from './types';

import { createSlice } from '@reduxjs/toolkit';

import * as actions from './actions';

const initialState: IUserStore = {
	user: null,
	isAuthChecked: false,
	isLoading: false,
	error: null,
};

export const userSlice = createSlice({
	name: 'user',
	initialState,
	reducers: {
		setIsAuthChecked: (state, action) => {
			state.isAuthChecked = action.payload;
		},
	},
	selectors: {
		getUser: (state) => state.user,
		getIsAuthChecked: (state) => state.isAuthChecked,
	},
	extraReducers: (builder) => {
		builder
			.addCase(actions.setUser, (state, action) => {
				state.user = action.payload || null;
			})
			.addCase(actions.loginUser.pending, (state) => {
				state.isLoading = true;
				state.error = null;
			})
			.addCase(actions.loginUser.fulfilled, (state, action) => {
				state.isLoading = false;
				state.user = action.payload.user;
				state.isAuthChecked = true;
			})
			.addCase(actions.loginUser.rejected, (state, action) => {
				state.isLoading = false;
				state.error = action.error?.message || 'Произошла ошибка';
			})
			.addCase(actions.registerUser.pending, (state) => {
				state.isLoading = true;
				state.error = null;
			})
			.addCase(actions.registerUser.fulfilled, (state) => {
				state.isLoading = false;
			})
			.addCase(actions.registerUser.rejected, (state, action) => {
				state.isLoading = false;
				state.error = action.error?.message || 'Произошла ошибка';
			})
			.addCase(actions.logoutUser.fulfilled, (state) => {
				state.user = null;
			});
	},
});

export const { setIsAuthChecked } = userSlice.actions;
export const { getIsAuthChecked, getUser } = userSlice.selectors;
