export interface ISelectProps<T> {
	options: T[];
	currentOption: T | null;
	onChooseOption: (option: T) => void;
	valueKey?: keyof T;
	labelKey?: keyof T;
	placeholder?: string;
}

export interface IMultiSelectProps<T> {
	options: T[];
	selectedOptions: T[];
	onChange: (selected: T[]) => void;
	valueKey?: keyof T;
	labelKey?: keyof T;
	placeholder?: string;
}
