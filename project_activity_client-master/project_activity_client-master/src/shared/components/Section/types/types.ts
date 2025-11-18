import type { ReactNode } from 'react';

export interface ISectionProps {
	sectionWidth?: 'default' | 'full' | 'large' | 'small';
	sectionHeight?: 'page' | 'card';
	sectionTitle?: ISectionTitle;
	sectionDescription?: string;
	withHeaderMargin?: boolean;
	children?: ReactNode;
}

export interface ISectionImgProps {
	sectionWidth?: 'default' | 'full' | 'large' | 'small';
	sectionTitle?: ISectionTitle;
	sectionDescription?: string;
	withIcon?: boolean;
	onIconClick?: () => void;
	children?: ReactNode;
}

interface ISectionTitle {
	text: string;
	size?: 'default' | 'large' | 'small';
}
