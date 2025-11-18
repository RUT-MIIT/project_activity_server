import type { ReactNode } from 'react';
import type { IBadge } from '../../Badge/types/types';
import type { IIcon } from '../../Icon/types/types';

export interface ILevelProps {
	title?: string;
	count?: number;
	icons?: IIcon[];
	isShow?: boolean;
	onShow?: () => void;
	children?: ReactNode;
}

export interface ILevelCardProps {
	id: number;
	name: string;
	description?: string;
	badges?: IBadge[];
	icons?: IIcon[];
	isActive?: boolean;
	isOpen?: boolean;
	onOpen?: (arg?: number | object) => void;
	children?: ReactNode;
}

export interface ILevelItemProps {
	id: number;
	name: string;
	badge?: {
		text: string;
		color: 'blue-dark' | 'blue-light' | 'blue' | 'green' | 'red' | 'grey';
	};
	mainColor?: 'blue' | 'grey' | 'default';
	controlColor?: 'blue' | 'green' | 'red' | 'grey' | 'default';
	level?: 'first' | 'second' | 'third';
	icons?: IIcon[];
	isActive?: boolean;
	isOpen?: boolean;
	isBlock?: boolean;
	onOpen?: (arg?: number | object) => void;
	children?: ReactNode;
}

export interface ILevelListProps {
	children?: ReactNode;
}

export interface ILevelEmptyProps {
	text: string;
}
