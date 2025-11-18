import type { FC } from 'react';

import { Outlet } from 'react-router-dom';
import { useDispatch, useSelector } from '../../../store/store';
import { useEffect } from 'react';

import { Tabs } from '../../../shared/components/Tabs/ui/tabs';
import { Section } from '../../../shared/components/Section';
import { Preloader } from '../../../shared/components/Preloader/ui/preloader';

import { getCoordinationAppsAction } from '../../../store/coordination/actions';
import { tabs } from '../lib/helpers';

export const CoordinationTabs: FC = () => {
	const dispatch = useDispatch();
	const { isLoadingApps } = useSelector((state) => state.coordination);

	useEffect(() => {
		dispatch(getCoordinationAppsAction());
	}, [dispatch]);

	if (isLoadingApps) return <Preloader />;

	return (
		<Section
			sectionWidth='full'
			sectionTitle={{ text: 'Согласование проектных заявок' }}
			sectionDescription='Проверяйте содержание, оставляйте комментарии и утверждайте заявки'
			withHeaderMargin>
			<Tabs tabs={tabs} />
			<Outlet />
		</Section>
	);
};
