import type { FC } from 'react';
import type { ITableProps } from '../types/types';

import styles from '../styles/table.module.scss';

export const TableRow: FC<ITableProps> = ({ children }) => {
	return <li className={styles.table__row}>{children}</li>;
};
