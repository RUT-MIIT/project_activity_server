import type { FC } from 'react';
import type { IContentTemplateProps } from '../types/types';

import styles from '../styles/content-template.module.scss';

export const ContentTemplate: FC<IContentTemplateProps> = ({
	type,
	text,
	id,
}) => {
	let content;

	switch (type) {
		case 'title':
			content = <h2 className={styles.text}>{text}</h2>;
			break;
		case 'nsi':
			content = (
				<p className={styles.text}>
					<span className={styles.text_bold}>[{id}] </span>
					{text}
				</p>
			);
			break;
		default:
			content = <p className={styles.text}>{text}</p>;
	}

	return <div className={styles.container}>{content}</div>;
};
