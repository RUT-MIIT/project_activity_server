import type { IApplicationItem } from '../../../store/application/types';

export interface ICoordinationAppProps {
	card: IApplicationItem;
}

export interface ICoordinationActiveAppsProps {
	apps: IApplicationItem[];
}
