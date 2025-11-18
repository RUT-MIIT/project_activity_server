import type { ReactNode } from 'react';

export interface ITableProps {
	children?: ReactNode;
}

export interface ITableColumnProps {
	text?: string | number;
	textWeight?: 'normal' | 'bold';
	columnType?: 'header' | 'default';
	columnSize: string;
}

export interface ITableControlProps {
	type?: 'default' | 'header';
	size?: number;
	children?: ReactNode;
}

export interface ITableTextProps {
	text: string;
	type?: 'default' | 'empty';
}
