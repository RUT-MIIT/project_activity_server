import type { FC } from 'react';
import type { IAppCardProps } from '../types/types';

import { useNavigate } from 'react-router-dom';
import { useSelector } from '../../../../../store/store';

import { Button } from '../../../../../shared/components/Button/ui/button';
import { Badge } from '../../../../../shared/components/Badge/ui/badge';

import { getStatusColor, getUserLevel } from '../../../lib/helpers';
import { getFullDate } from '../../../../../shared/lib/date';
import { EPAGESROUTES, EMAINROUTES } from '../../../../../shared/utils/routes';

import styles from '../styles/app-card.module.scss';

export const AppCard: FC<IAppCardProps> = ({ card, withAuthor = false }) => {
	const navigate = useNavigate();

	const { user } = useSelector((state) => state.user);

	const showDetailApp = () => {
		navigate(`${EPAGESROUTES.MAIN}/${EMAINROUTES.COORDINATION}/app/${card.id}`);
	};

	const level = getUserLevel(user?.role || 'user');
	const color = getStatusColor(card.status.code, level);

	return (
		<li className={styles.card} key={card.id}>
			<div className={styles.card__header}>
				<Badge text={card.status.name} color={color} />
			</div>
			<div className={styles.card__main}>
				<h4 className={styles.card__title}>{card.title}</h4>
				<p className={styles.card__text}>{card.company}</p>
				{withAuthor && (
					<div className={styles.card__author}>
						<div className={styles.card__column}>
							<p
								className={`${styles.card__text} ${styles.card__text_color_grey}`}>
								Автор
							</p>
							<p className={styles.card__text}>{card.author_name}</p>
						</div>
						<div className={styles.card__column}>
							<p
								className={`${styles.card__text} ${styles.card__text_color_grey}`}>
								Почта
							</p>
							<p className={styles.card__text}>{card.author_email}</p>
						</div>
					</div>
				)}
				<p className={`${styles.card__text} ${styles.card__text_color_grey}`}>
					Дата подачи: {getFullDate(card.creation_date)}
				</p>
			</div>
			<div className={styles.card__footer}>
				<Button text='История изменения' color='cancel' />
				<Button text='Просмотр' onClick={showDetailApp} />
			</div>
		</li>
	);
};
