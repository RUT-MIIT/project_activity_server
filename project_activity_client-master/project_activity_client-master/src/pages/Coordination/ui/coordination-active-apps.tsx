import type { FC } from 'react';
import type { ICoordinationActiveAppsProps } from '../types/types';

import { AppCard } from '../../Application/components/AppCard/ui/app-card';
import { Text } from '../../../shared/components/Typography';

import styles from '../styles/coordination.module.scss';

export const CoordinationActiveApps: FC<ICoordinationActiveAppsProps> = ({
	apps,
}) => {
	return apps.length > 0 ? (
		<ul className={styles.list}>
			{apps.map((app) => (
				<AppCard card={app} key={app.id} withAuthor />
			))}
		</ul>
	) : (
		<Text text='Заявки не найдены.' color='grey' withMarginTop />
	);
};
