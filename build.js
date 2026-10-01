const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, LevelFormat, Footer, PageNumber } = require('docx');
const F = "Times New Roman";
const runs = (s, size = 24, extra = {}) => s.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(t =>
  t.startsWith('**') ? new TextRun({ text: t.slice(2, -2), bold: true, font: F, size, ...extra }) : new TextRun({ text: t, font: F, size, ...extra }));
const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(caption, head, body) {
  const n = head.length, W = 9026, w = Math.floor(W / n), cw = Array(n).fill(w); cw[0] += W - w * n;
  const cell = (t, i, h) => new TableCell({ borders, width: { size: cw[i], type: WidthType.DXA }, margins: { top: 50, bottom: 50, left: 80, right: 80 },
    shading: h ? { fill: "E7E6E6", type: ShadingType.CLEAR } : undefined, children: [new Paragraph({ children: [new TextRun({ text: t, font: F, size: 20, bold: h })] })] });
  return [new Paragraph({ spacing: { before: 120, after: 80 }, children: [new TextRun({ text: caption, font: F, size: 22, bold: true })] }),
    new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, rows: [head, ...body].map((r, ri) => new TableRow({ children: r.map((t, i) => cell(t, i, ri === 0)) })) }),
    new Paragraph({ spacing: { after: 160 }, children: [] })];
}
const T1 = table("Table 1. Model awareness and prominence by brand and platform [template]",
  ["Brand (type)", "Platform", "Mention rate", "Share-of-model", "First-mention rate", "Avg. position"],
  [["[Brand A] (D2C)", "ChatGPT", "", "", "", ""], ["[Brand A] (D2C)", "Perplexity", "", "", "", ""], ["[Brand B] (Incumbent)", "ChatGPT", "", "", "", ""], ["...", "", "", "", "", ""]]);
const T2 = table("Table 2. Citation mix by brand type [template]",
  ["Brand type", "Brand-owned", "Marketplace", "Review/ community", "Editorial/ press", "Encyclopaedic"],
  [["D2C brands", "", "", "", "", ""], ["Incumbents", "", "", "", "", ""]]);
const out = [];
for (const line of fs.readFileSync('chapter.md', 'utf8').split('\n')) {
  if (!line.trim()) continue;
  if (line.startsWith('@TITLE ')) out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: line.slice(7), font: F, size: 32, bold: true })] }));
  else if (line.startsWith('@CENTER ')) out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: runs(line.slice(8)) }));
  else if (line.startsWith('@NOTE ')) out.push(new Paragraph({ spacing: { before: 200, after: 200 }, shading: { fill: "FFF2CC", type: ShadingType.CLEAR }, children: runs(line.slice(6), 21, { italics: true }) }));
  else if (line === '@TABLE1') out.push(...T1);
  else if (line === '@TABLE2') out.push(...T2);
  else if (line.startsWith('@REF ')) out.push(new Paragraph({ spacing: { after: 120, line: 276 }, indent: { left: 720, hanging: 720 }, children: runs(line.slice(5), 22) }));
  else if (line.startsWith('## ')) out.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 220, after: 100 }, children: [new TextRun({ text: line.slice(3), font: F, size: 24, bold: true, color: "000000" })] }));
  else if (line.startsWith('# ')) out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 140 }, children: [new TextRun({ text: line.slice(2), font: F, size: 26, bold: true, color: "000000" })] }));
  else if (line.startsWith('- ')) out.push(new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 80, line: 300 }, alignment: AlignmentType.JUSTIFIED, children: runs(line.slice(2)) }));
  else out.push(new Paragraph({ spacing: { after: 160, line: 300 }, alignment: AlignmentType.JUSTIFIED, children: runs(line, 24, line.startsWith('[') ? { italics: true, color: "7F6000" } : {}) }));
}
const doc = new Document({ styles: { default: { document: { run: { font: F, size: 24 } } } },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] }] },
  sections: [{ properties: { page: { margin: { top: 1300, bottom: 1300, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: F, size: 20 })] })] }) }, children: out }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync("Book_Chapter_Draft.docx", b));
