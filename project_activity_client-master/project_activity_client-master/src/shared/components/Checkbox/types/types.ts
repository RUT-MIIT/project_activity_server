export interface ICheckboxProps {
	checked: boolean;
	label?: string;
	onChange: (checked: boolean) => void;
	disabled?: boolean;
}
