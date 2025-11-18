import type { ReactNode } from 'react';

export interface ITextProps {
	text: string;
	color?: 'black' | 'grey' | 'white';
	withMarginTop?: boolean;
}

export interface IContainerProps {
	children?: ReactNode;
}

export interface IListProps {
	title: string;
	items: IListItem[];
}

export interface IListItem {
	title: string;
	text: string;
}
