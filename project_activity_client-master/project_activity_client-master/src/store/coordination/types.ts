import type {
	IApplicationItem,
	IApplicationDetail,
	IField,
} from '../application/types';

export interface ICoordinationStore {
	application: IApplicationItem | null;
	applications: IApplicationItem[];
	applicationDetail: IApplicationDetail | null;
	currentField: IField | null;
	isLoadingApps: boolean;
	isLoadingDetail: boolean;
	isLoadingComment: boolean;
	error: string | null;
}

export interface ICreateCommentAction {
	applicationId: number;
	field: string;
	text: string;
}

export interface IAppActionResponse {
	message: string;
	status: string;
	status_name: string;
}
