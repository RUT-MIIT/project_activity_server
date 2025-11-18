import type { FC } from 'react';

import styles from '../styles/parse-text.module.scss';

interface IParseTextProps {
	text: string;
}

interface IParsedParagraph {
	text: string;
	type: 'title' | 'paragraph';
}

export const ParseText: FC<IParseTextProps> = ({ text }) => {
	const parseText = (input: string) => {
		const paragraphs = input.split(/\n\n+/);

		const parsedParagraphs: IParsedParagraph[] = paragraphs.map((paragraph) => {
			if (paragraph.startsWith('####')) {
				return { text: paragraph.slice(4).trim(), type: 'title' };
			}
			if (paragraph.startsWith('**')) {
				return { text: paragraph, type: 'title' };
			}
			return { text: paragraph.trim(), type: 'paragraph' };
		});

		return { parsedParagraphs };
	};

	const { parsedParagraphs } = parseText(text);

	return parsedParagraphs.length > 0 ? (
		<ul className={styles.list}>
			{parsedParagraphs.map((paragraph, index) => (
				<li className={styles.item} key={index}>
					{paragraph.type === 'title' ? (
						<h4 className={styles.title}>{paragraph.text}</h4>
					) : (
						<p className={styles.text}>{paragraph.text}</p>
					)}
				</li>
			))}
		</ul>
	) : (
		<p className={styles.text}>{text}</p>
	);
};
