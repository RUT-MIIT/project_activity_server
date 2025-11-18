import type { FC } from 'react';
import type { ILevelItemProps } from '../../types/types';

import { Icon } from '../../../Icon/ui/icon';

import styles from './level-item.module.scss';

export const LevelItem: FC<ILevelItemProps> = ({
	id,
	name,
	badge = { text: '', color: 'blue' },
	mainColor = 'default',
	controlColor = 'blue',
	level = 'first',
	isActive = false,
	isOpen,
	onOpen,
	isBlock = false,
	icons,
	children,
}) => {
	return (
		<li
			id={`data-id-${id}`}
			className={`${styles.item} ${isActive ? styles.item_active : ''} ${
				isOpen ? styles.item_open : ''
			} ${styles[`item_level_${level}`]}`}>
			{isBlock ? (
				<>
					<div
						className={`${styles.badge} ${styles.badge_type_block}`}
						onClick={onOpen}>
						<span className={styles.badge__text}>{badge.text}</span>
					</div>
					<div
						className={`${styles.main} ${styles.main_type_block}`}
						onClick={onOpen}>
						<h4 className={styles.title}>{name}</h4>
						{children}
					</div>
					<div
						className={`${styles.control} ${styles.control_type_block}`}></div>
				</>
			) : (
				<>
					<div
						className={`${styles.badge} ${
							styles[`badge_color_${badge.color}`]
						}`}
						onClick={onOpen}>
						<span className={styles.badge__text}>{badge.text}</span>
					</div>
					<div
						className={`${styles.main} ${styles[`main_color_${mainColor}`]}`}
						onClick={onOpen}>
						<h4 className={styles.title}>{name}</h4>
						{children}
					</div>
					<div
						className={`${styles.control} ${
							styles[`control_color_${controlColor}`]
						}`}>
						{icons?.map((elem, i) => (
							<Icon
								key={i}
								icon={elem.icon}
								color={elem.color}
								onClick={elem.onClick}
							/>
						))}
					</div>
				</>
			)}
		</li>
	);
};
