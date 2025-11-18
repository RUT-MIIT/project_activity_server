import type { CSSProperties } from 'react';

export interface IButtonProps {
	text: string;
	type?: 'button' | 'submit' | 'link';
	form?: string;
	href?: string;
	style?: CSSProperties;
	color?: 'default' | 'blue' | 'white' | 'confirm' | 'cancel' | 'green' | 'red';
	withIcon?: {
		type:
			| 'add'
			| 'confirm'
			| 'next'
			| 'prev'
			| 'send'
			| 'check'
			| 'back'
			| 'return'
			| 'cancel';
		position?: 'left' | 'right';
		color?: 'black' | 'white' | 'blue' | 'grey';
	};
	width?: 'default' | 'full' | 'auto';
	isBlock?: boolean;
	onClick?: () => void;
}
