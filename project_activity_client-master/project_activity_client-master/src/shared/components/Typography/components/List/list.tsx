import type { FC } from 'react';
import type { IListProps, IListItem } from '../../types/types';

import styles from '../../styles/typography.module.scss';

export const List: FC<IListProps> = ({ title, items }) => {
	return (
		<>
			{title && <h4 className={styles.list__title}>{title}</h4>}
			<ul className={styles.list}>
				{items.map((item: IListItem, i: number) => (
					<li className={styles.item} key={i}>
						<h6 className={styles.item__title}>{`${i + 1}. ${item.title}`}</h6>
						<p className={styles.item__text}>{item.text}</p>
					</li>
				))}
			</ul>
		</>
	);
};
