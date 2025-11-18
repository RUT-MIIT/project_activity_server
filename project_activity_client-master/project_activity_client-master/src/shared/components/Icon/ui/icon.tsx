import type { FC } from 'react';
import type { IIcon } from '../types/types';

import styles from '../styles/icon.module.scss';

export const Icon: FC<IIcon> = ({
	icon,
	type = 'button',
	color = 'grey',
	onClick,
}) => {
	return type === 'elem' ? (
		<div
			className={`${styles.icon} ${styles[`icon_icon_${icon}`]} ${
				styles[`icon_color_${color}`]
			}`}></div>
	) : (
		<button
			className={`${styles.icon} ${styles.icon_active} ${
				styles[`icon_icon_${icon}`]
			} ${styles[`icon_color_${color}`]}`}
			onClick={onClick}
			type='button'></button>
	);
};
