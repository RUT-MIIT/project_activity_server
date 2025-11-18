export interface ITab {
	label: string;
	path: string;
	disabled?: boolean;
}

export interface ITabsProps {
	tabs: ITab[];
	activeTab?: string;
	onTabChange?: (path: string) => void;
}
