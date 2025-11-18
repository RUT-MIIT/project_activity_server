import type { FC } from 'react';
import type { ILevelEmptyProps } from '../../types/types';

import styles from './level-empty.module.scss';

export const LevelEmpty: FC<ILevelEmptyProps> = ({ text }) => {
	return <span className={styles.text}>{text}</span>;
};
