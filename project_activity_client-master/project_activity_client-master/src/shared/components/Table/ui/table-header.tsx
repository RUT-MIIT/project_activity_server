import type { FC } from 'react';
import type { ITableProps } from '../types/types';

import { TableMainColumn } from './table-main-column';
import { TableControl } from './table-control';

import styles from '../styles/table.module.scss';

export const TableHeader: FC<ITableProps> = ({ children }) => {
	return (
		<div className={styles.table__header}>
			<TableMainColumn>{children}</TableMainColumn>
			<TableControl type='header' size={2} />
		</div>
	);
};
