export interface IBadge {
	text: string;
	type?: 'elem' | 'button';
	color?: string;
	onClick?: () => void;
}
