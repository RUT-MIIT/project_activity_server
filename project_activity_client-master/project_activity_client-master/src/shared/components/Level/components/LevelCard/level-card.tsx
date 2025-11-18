import type { FC } from 'react';
import type { ILevelCardProps } from '../../types/types';

import { Badge } from '../../../Badge/ui/badge';
import { Icon } from '../../../Icon/ui/icon';

import styles from './level-card.module.scss';

export const LevelCard: FC<ILevelCardProps> = ({
	id,
	name,
	description,
	badges,
	isActive = false,
	isOpen,
	onOpen,
	icons,
	children,
}) => {
	return (
		<li
			id={`data-id-${id}`}
			className={`
				${styles.card}
				${isActive ? styles.card_active : ''}
				${isOpen ? styles.card_open : ''}
			`}
			onClick={onOpen}>
			<div className={styles.header}>
				{badges?.map((badge, i) => (
					<Badge key={i} text={badge.text} />
				))}
				<div className={styles.control}>
					{icons?.map((elem, i) => (
						<Icon key={i} icon={elem.icon} onClick={elem.onClick} />
					))}
				</div>
			</div>
			<div className={styles.main}>
				<h4 className={styles.title}>{name}</h4>
				{description && <p className={styles.description}>{description}</p>}
				{children}
			</div>
		</li>
	);
};
