import type { FC } from 'react';
import type { IFormLinksProps, IFormLink } from '../../types/types';

import { NavLink } from 'react-router-dom';

import styles from './form-links.module.scss';

export const FormLinks: FC<IFormLinksProps> = ({ links }) => {
	return (
		<nav className={styles.container}>
			{links.map((elem: IFormLink, i: number) => (
				<div className={styles.item} key={i}>
					{elem.label && <p className={styles.label}>{elem.label}</p>}
					<NavLink className={styles.link} to={elem.url}>
						{elem.text}
					</NavLink>
				</div>
			))}
		</nav>
	);
};
