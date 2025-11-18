import { combineSlices } from '@reduxjs/toolkit';
import { userSlice } from './user/reducer';
import { catalogSlice } from './catalog/reducer';
import { applicationSlice } from './application/reducer';
import { coordinationSlice } from './coordination/reducer';
import { controlApproveSlice } from './control-approve/reducer';

export const rootReducer = combineSlices(
	userSlice,
	catalogSlice,
	applicationSlice,
	coordinationSlice,
	controlApproveSlice
);
