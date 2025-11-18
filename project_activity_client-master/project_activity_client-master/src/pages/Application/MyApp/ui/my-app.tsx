import type { FC } from 'react';
import type { IApplicationItem } from '../../../../store/application/types';

import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from '../../../../store/store';

import { Section } from '../../../../shared/components/Section/ui/section';
import { Preloader } from '../../../../shared/components/Preloader/ui/preloader';
import { Filter } from '../../../../shared/components/Filter/ui/filter';
import { Button } from '../../../../shared/components/Button/ui/button';
import { Text } from '../../../../shared/components/Typography';
import { AppCard } from '../../components/AppCard/ui/app-card';

import { getAppsAction } from '../../../../store/application/actions';
import { EPAGESROUTES, EMAINROUTES } from '../../../../shared/utils/routes';

import styles from '../styles/my-app.module.scss';

export const MyApp: FC = () => {
	const navigate = useNavigate();
	const dispatch = useDispatch();
	const { applications, isLoading } = useSelector((state) => state.application);
	const [filteredApps, setFilteredApps] = useState<IApplicationItem[]>([]);

	const createNewApp = () => {
		navigate(`${EPAGESROUTES.MAIN}/${EMAINROUTES.NEW_APP}`, {
			replace: true,
		});
	};

	useEffect(() => {
		dispatch(getAppsAction());
	}, [dispatch]);

	useEffect(() => {
		setFilteredApps(
			[...applications].sort(
				(a, b) =>
					new Date(b.creation_date).getTime() -
					new Date(a.creation_date).getTime()
			)
		);
	}, [applications]);

	return (
		<Section
			sectionWidth='full'
			sectionTitle={{ text: 'Мои заявки' }}
			sectionDescription='Следите за статусом и обновляйте ваши заявки'
			withHeaderMargin>
			{isLoading ? (
				<Preloader />
			) : (
				<>
					<div className={styles.header}>
						<Filter<IApplicationItem>
							data={applications}
							searchKey='title'
							placeholder='Поиск по названию...'
							onFilter={setFilteredApps}
						/>
						<Button
							text='Новая заявка'
							color='blue'
							withIcon={{
								type: 'add',
								position: 'left',
								color: 'white',
							}}
							onClick={createNewApp}
						/>
					</div>
					{filteredApps.length > 0 ? (
						<ul className={styles.list}>
							{filteredApps.map((item) => (
								<AppCard card={item} key={item.id} />
							))}
						</ul>
					) : (
						<Text
							text='По заданным параметрам ничего не найдено'
							color='grey'
							withMarginTop
						/>
					)}
				</>
			)}
		</Section>
	);
};
