import type { FC } from 'react';
import type { ILinkProps } from '../types/types';

import styles from '../styles/link.module.scss';

export const Link: FC<ILinkProps> = ({ text, path }) => {
	return (
		<a className={styles.link} href={path} target='_blank' rel='noreferrer'>
			{text}
		</a>
	);
};
