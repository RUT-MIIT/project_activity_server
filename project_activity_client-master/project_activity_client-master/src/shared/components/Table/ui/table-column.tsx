import type { FC } from 'react';
import type { ITableColumnProps } from '../types/types';

import styles from '../styles/table.module.scss';

export const TableColumn: FC<ITableColumnProps> = ({
	text,
	textWeight = 'normal',
	columnType = 'default',
	columnSize,
}) => {
	return (
		<div
			className={`${styles.table__column} ${
				styles[`table__column_type_${columnType}`]
			} ${columnSize ? styles[`table__column_size_${columnSize}`] : ''}`}>
			<p
				className={`${styles.table__text} ${
					styles[`table__text_weight_${textWeight}`]
				}`}>
				{text}
			</p>
		</div>
	);
};
