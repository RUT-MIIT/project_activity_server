import type { FC } from 'react';
import type { ITableControlProps } from '../types/types';

import styles from '../styles/table.module.scss';

export const TableControl: FC<ITableControlProps> = ({
	children,
	size = 0,
	type = 'default',
}) => {
	return type === 'default' ? (
		<div className={styles.table__control}>{children}</div>
	) : (
		<div
			className={`${styles.table__control} ${styles.table__control_type_header}`}>
			{Array.from({ length: size }).map((_, index) => (
				<div key={index} className={styles.table__btn_stub}></div>
			))}
		</div>
	);
};
