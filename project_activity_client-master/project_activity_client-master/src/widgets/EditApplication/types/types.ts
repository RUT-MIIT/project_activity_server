import type { PropsWithChildren } from 'react';
import type { IField } from '../../../store/application/types';

export interface IEditAppForm {
	title: string;
	company: string;
	company_contacts: string;
	project_level: { id: number; name: string };
	target_institutes: { code: string; name: string }[];

	problem_holder: string;
	goal: string;
	barrier: string;
	existing_solutions: string;

	context: string;
	recommended_tools: string;
	stakeholders: string;
	experts: string;
	additional_materials: string;
}

export interface IApplicationFieldProps extends PropsWithChildren {
	title: string;
	fieldCode: string;
	currentField?: IField | null;
	getCommentCount: (fieldName: string) => number;
	onSelectField: (field: IField) => void;
}
