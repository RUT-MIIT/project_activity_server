import type { FC } from 'react';
import type { ITextProps } from '../../types/types';

import styles from '../../styles/typography.module.scss';

export const Text: FC<ITextProps> = ({
	text,
	color = 'black',
	withMarginTop = false,
}) => {
	return (
		<p
			className={`${styles.text} ${styles[`text_color_${color}`]} ${
				withMarginTop ? styles.text_margin_top : ''
			}`}>
			{text}
		</p>
	);
};
