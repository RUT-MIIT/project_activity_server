export interface IFilterProps<T> {
	data: T[];
	searchKey: keyof T;
	placeholder?: string;
	onFilter: (filtered: T[]) => void;
}
