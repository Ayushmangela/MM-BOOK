// Builds the chapter .docx from chapter.md.  Usage: node build.js [chapter.md] [output.docx]
//
// Line syntax
//   @TITLE text            chapter title           @CENTER text   centred line
//   @NOTE text             yellow internal note (must be removed before submission)
//   # HEADING 1            bold, ALL CAPS (IGI)    ## Heading 2   bold, title case
//   ### Heading 3          italic, title case      - bullet       1. numbered item
//   @REF text              APA reference, hanging indent
//   @QUOTE text            indented verbatim excerpt
//   @FIG path | caption    figure (PNG), scaled to text width, caption below
//   @TABLE path.csv | caption | note    table built from a CSV, caption above, note below
//   @PAGEBREAK
// Inline: **bold**, *italic*. Text in [square brackets] at line start is shown as a placeholder.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, LevelFormat, Footer, PageNumber, ImageRun, PageBreak } = require('docx');

const SRC = process.argv[2] || 'chapter.md';
const OUT = process.argv[3] || 'Book_Chapter_Generative_Brand_Equity.docx';
const F = 'Times New Roman';
const TEXT_W_IN = 6.27; // A4 width minus 1-inch margins

function runs(s, size = 24, extra = {}) {
  const out = [];
  for (const part of s.split(/(\*\*[^*]+\*\*)/).filter(Boolean)) {
    if (part.startsWith('**') && part.endsWith('**')) {
      out.push(...italics(part.slice(2, -2), size, { ...extra, bold: true }));
    } else out.push(...italics(part, size, extra));
  }
  return out;
}
function italics(s, size, extra) {
  return s.split(/(\*[^*\s][^*]*\*)/).filter(Boolean).map(t =>
    t.length > 2 && t.startsWith('*') && t.endsWith('*')
      ? new TextRun({ text: t.slice(1, -1), italics: true, font: F, size, ...extra })
      : new TextRun({ text: t, font: F, size, ...extra }));
}

function parseCSV(text) {
  const rows = []; let row = [], cur = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"' && text[i + 1] === '"') { cur += '"'; i++; }
      else if (c === '"') q = false; else cur += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(cur); cur = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cur); cur = ''; if (row.some(x => x !== '')) rows.push(row); row = [];
    } else cur += c;
  }
  if (cur !== '' || row.length) { row.push(cur); if (row.some(x => x !== '')) rows.push(row); }
  return rows;
}

const thin = { style: BorderStyle.SINGLE, size: 4, color: '000000' };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

function csvTable(file, caption, note) {
  const rows = parseCSV(fs.readFileSync(file, 'utf8'));
  const head = rows[0], body = rows.slice(1), n = head.length;
  const W = 9026;
  // width proportional to the longest cell in each column (bounded)
  const len = head.map((h, j) => Math.min(38, Math.max(6, ...rows.map(r => (r[j] || '').length))));
  const tot = len.reduce((a, b) => a + b, 0);
  const cw = len.map(l => Math.floor(W * l / tot)); cw[0] += W - cw.reduce((a, b) => a + b, 0);
  const numeric = s => /^[-–]?[\d.,]+%?$|^[\d.]+ \[|^\d/.test(s.trim());
  const cell = (t, j, isHead, isLast) => new TableCell({
    width: { size: cw[j], type: WidthType.DXA }, margins: { top: 30, bottom: 30, left: 70, right: 70 },
    borders: { top: isHead ? thin : none, bottom: (isHead || isLast) ? thin : none, left: none, right: none },
    children: [new Paragraph({ alignment: (!isHead && j > 0 && numeric(t)) ? AlignmentType.RIGHT : AlignmentType.LEFT,
      children: runs(t, 19, isHead ? { bold: true } : {}) })] });
  const out = [new Paragraph({ keepNext: true, spacing: { before: 200, after: 80 }, children: runs(caption, 21, {}) })];
  out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw,
    rows: [head, ...body].map((r, i) => new TableRow({ cantSplit: true, tableHeader: i === 0,
      children: r.map((t, j) => cell(t, j, i === 0, i === body.length)) })) }));
  if (note) out.push(new Paragraph({ spacing: { before: 60, after: 200 }, children: runs(note, 18, {}) }));
  else out.push(new Paragraph({ spacing: { after: 160 }, children: [] }));
  return out;
}

function figure(file, caption) {
  const buf = fs.readFileSync(file);
  // PNG IHDR gives pixel size; dpi assumed 300
  const wpx = buf.readUInt32BE(16), hpx = buf.readUInt32BE(20);
  let wIn = Math.min(TEXT_W_IN, wpx / 300);
  const wPt = Math.round(wIn * 96), hPt = Math.round(wIn * 96 * hpx / wpx);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 200, after: 80 },
      children: [new ImageRun({ type: 'png', data: buf, transformation: { width: wPt, height: hPt },
        altText: { title: caption.split('.')[0], description: caption, name: path.basename(file) } })] }),
    new Paragraph({ spacing: { after: 240 }, children: runs(caption, 21, {}) }),
  ];
}

const out = [];
let numberedRef = 0;
for (const raw of fs.readFileSync(SRC, 'utf8').split('\n')) {
  const line = raw.replace(/\s+$/, '');
  if (!line.trim()) continue;
  if (line.startsWith('<!--')) continue;
  if (line.startsWith('@TITLE ')) out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: runs(line.slice(7), 32, { bold: true }) }));
  else if (line.startsWith('@CENTER ')) out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: runs(line.slice(8)) }));
  else if (line.startsWith('@NOTE ')) out.push(new Paragraph({ spacing: { before: 200, after: 200 }, shading: { fill: 'FFF2CC', type: ShadingType.CLEAR }, children: runs(line.slice(6), 21, { italics: true }) }));
  else if (line === '@PAGEBREAK') out.push(new Paragraph({ children: [new PageBreak()] }));
  else if (line.startsWith('@FIG ')) { const [f, c] = line.slice(5).split(' | '); out.push(...figure(f.trim(), c.trim())); }
  else if (line.startsWith('@TABLE ')) { const [f, c, n] = line.slice(7).split(' | '); out.push(...csvTable(f.trim(), c.trim(), n && n.trim())); }
  else if (line.startsWith('@REF ')) out.push(new Paragraph({ spacing: { after: 100, line: 264 }, indent: { left: 720, hanging: 720 }, children: runs(line.slice(5), 22) }));
  else if (line.startsWith('@QUOTE ')) out.push(new Paragraph({ spacing: { after: 160, line: 276 }, indent: { left: 720, right: 720 }, alignment: AlignmentType.JUSTIFIED, children: runs(line.slice(7), 22) }));
  else if (line.startsWith('### ')) out.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, spacing: { before: 200, after: 80 }, children: [new TextRun({ text: line.slice(4), font: F, size: 24, italics: true, color: '000000' })] }));
  else if (line.startsWith('## ')) out.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 240, after: 100 }, children: [new TextRun({ text: line.slice(3), font: F, size: 24, bold: true, color: '000000' })] }));
  else if (line.startsWith('# ')) out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, keepNext: true, spacing: { before: 360, after: 140 }, children: [new TextRun({ text: line.slice(2).toUpperCase(), font: F, size: 26, bold: true, color: '000000' })] }));
  else if (line.startsWith('- ')) out.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 80, line: 300 }, alignment: AlignmentType.JUSTIFIED, children: runs(line.slice(2)) }));
  else if (/^\d+\. /.test(line)) out.push(new Paragraph({ numbering: { reference: 'num', level: 0 }, spacing: { after: 80, line: 300 }, alignment: AlignmentType.JUSTIFIED, children: runs(line.replace(/^\d+\. /, '')) }));
  else out.push(new Paragraph({ spacing: { after: 160, line: 300 }, alignment: AlignmentType.JUSTIFIED,
    children: runs(line, 24, line.startsWith('[') ? { color: '7F6000' } : {}) }));
}

const doc = new Document({
  creator: 'Authors', title: 'Generative Brand Equity',
  styles: { default: { document: { run: { font: F, size: 24 } } } },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: F, size: 20 })] })] }) },
    children: out }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log(`wrote ${OUT}`); });
