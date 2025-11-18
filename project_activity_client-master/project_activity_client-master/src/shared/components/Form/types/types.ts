import type { ReactNode, FormEventHandler, ChangeEvent } from 'react';

export interface IFormProps {
	title?: string;
	subtitle?: string;
	titleAlign?: 'center' | 'left';
	formWidth?: 'full' | 'large' | 'default' | 'small';
	withHeightStretch?: boolean;
	name: string;
	onSubmit?: FormEventHandler<HTMLFormElement>;
	children?: ReactNode;
}

export interface IFormFieldProps {
	title?: string;
	withInfo?: boolean;
	withMarginBottom?: boolean;
	onInfo?: () => void;
	fieldError?: IFormFieldError;
	children?: ReactNode;
}

export interface IFormFieldError {
	text: string;
	isShow: boolean;
}

export interface IFormInputProps {
	type?: 'text' | 'number';
	name: string;
	placeholder?: string;
	value: string;
	onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

export interface IFormInputNumberProps {
	type?: 'number';
	name: string;
	placeholder?: string;
	value: number | null;
	onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

export interface IFormTextareaProps {
	name: string;
	placeholder?: string;
	value: string;
	onChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
}

export interface IFormButtonsProps {
	children?: ReactNode;
}

export interface IFormLink {
	text: string;
	label: string;
	url: string;
}

export interface IFormLinksProps {
	links: IFormLink[];
}

export type TFormValidationErrors = Record<string, string | undefined>;
