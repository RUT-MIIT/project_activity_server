import type { ReactNode } from 'react';

export interface ICardProps {
	title?: string;
	subtitle?: string;
	withHeightStretch?: boolean;
	children?: ReactNode;
}
