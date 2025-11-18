import type { FC } from 'react';

import { useNavigate } from 'react-router-dom';
import { useSelector } from '../../../store/store';

import { Button } from '../../../shared/components/Button/ui/button';

import { getUser } from '../../../store/user/reducer';

import { EPAGESROUTES, EMAINROUTES } from '../../../shared/utils/routes';

import styles from '../styles/home.module.scss';

export const Home: FC = () => {
	const navigate = useNavigate();
	const user = useSelector(getUser);

	const createNewApp = () => {
		navigate(`${EPAGESROUTES.MAIN}/${EMAINROUTES.NEW_APP}`, {
			replace: true,
		});
	};

	return (
		user && (
			<div className={styles.home}>
				<div className={styles.header}>
					<div className={styles.header__info}>
						<h1 className={styles.header__title}>
							Добро пожаловать, {user.last_name} {user.first_name}
						</h1>
						<p className={styles.header__subtitle}>
							Вот что актуально на сегодня
						</p>
					</div>
					<Button
						text='Новая заявка'
						color='white'
						withIcon={{ type: 'add', position: 'left', color: 'blue' }}
						onClick={createNewApp}
					/>
				</div>
			</div>
		)
	);
};
