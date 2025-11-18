export interface IApplicationStore {
	application: IApplication | null;
	applications: IApplicationItem[];
	isLoading: boolean;
	error: string | null;
}

export interface ICreateAppMain {
	author: number;
	author_firstname: string;
	author_middlename: string;
	author_lastname: string;
	author_phone: string;
	author_email: string;
	author_role: string;
	author_division: string;

	title: string;
	company: string;
	company_contacts: string;
	project_level: string;
	target_institutes: string[];

	problem_holder: string;
	goal: string;
	barrier: string;
	existing_solutions: string;

	context: string;
	stakeholders: string;
	recommended_tools: string;
	experts: string;
	additional_materials: string;
	needs_consultation: boolean;
}

export interface ICreateAppPublic {
	author_firstname: string;
	author_middlename: string;
	author_lastname: string;
	author_phone: string;
	author_email: string;

	company: string;
	company_contacts: string;
	target_institutes: { code: string; name: string }[];

	problem_holder: string;
	goal: string;
	barrier: string;
	existing_solutions: string;
}

export interface IEditApp {
	title: string;
	company: string;
	company_contacts: string;
	project_level: string;
	target_institutes: string[];

	problem_holder: string;
	goal: string;
	barrier: string;
	existing_solutions: string;

	context: string;
	stakeholders: string;
	recommended_tools: string;
	experts: string;
	additional_materials: string;
}

export interface IApplication {
	id: number;
	title: string;
	creation_date: string;
	status: { code: string; name: string };

	author: number;
	author_division: string;
	author_firstname: string;
	author_middlename: string;
	author_lastname: string;
	author_phone: string;
	author_email: string;
	author_role: string;

	company: string;
	company_contacts: string;
	project_level: string;
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
	needs_consultation: boolean;
}

export interface IApplicationItem {
	author_email: string;
	author_name: string;
	company: string;
	creation_date: string;
	id: number;
	needs_consultation: boolean;
	status: { code: string; name: string };
	title: string;
}

export interface IApplicationDetail extends IApplication {
	involved_users: {
		id: number;
		user: { id: number; name: string; email: string };
		added_at: string;
		added_by: { id: number; name: string };
	};
	involved_departments: {
		id: number;
		department: { id: number; name: string; short_name: string };
		added_at: string;
		added_by: { id: number; name: string };
	};
	comments: IApplicationComment[];
	available_actions: {
		action: string;
		label: string;
		config: {
			status_code: string;
		};
	}[];
}

export interface IApplicationComment {
	field: string;
	text: string;
	author: {
		id: number;
		name: string;
		short_name: string;
		role_name: string;
		department_name: string;
	};
	created_at: string;
	id: number;
}

export interface IField {
	name: string;
	code: string;
}
