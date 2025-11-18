export interface ICreateAppMainForm {
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
	needs_consultation: boolean;
}
