import type { FC } from 'react';
import type { IBadge } from '../types/types';

import styles from '../styles/badge.module.scss';

export const Badge: FC<IBadge> = ({
	text,
	color = 'blue',
	type = 'elem',
	onClick,
}) => {
	return type === 'elem' ? (
		<div className={`${styles.badge} ${styles[`badge_color_${color}`]}`}>
			{text}
		</div>
	) : (
		<button
			className={`${styles.badge} ${styles.badge_active} ${
				styles[`badge_color_${color}`]
			}`}
			onClick={onClick}
			type='button'>
			{text}
		</button>
	);
};
