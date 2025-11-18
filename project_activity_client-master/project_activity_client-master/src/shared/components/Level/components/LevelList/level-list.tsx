import type { FC } from 'react';
import type { ILevelListProps } from '../../types/types';

import styles from './level-list.module.scss';

export const LevelList: FC<ILevelListProps> = ({ children }) => {
	return <ul className={styles.list}>{children}</ul>;
};
