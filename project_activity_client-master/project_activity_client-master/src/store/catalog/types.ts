export interface ICatalogStore {
	institutes: IInstitute[];
	departments: IDepartment[];
	roles: IRole[];
	isLoadingCatalog: boolean;
	error: string | null;
}

export interface IInstitute {
	code: string;
	name: string;
}

export interface IDepartment {
	id: number;
	name: string;
	short_name: string;
}

export interface IRole {
	code: string;
	name: string;
}
