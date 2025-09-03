#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF封面添加脚本
将cover.jpg添加到site/pdf/document.pdf的第一页，并输出到脚本同目录下
"""

import os
import sys
from pathlib import Path
try:
    from PyPDF2 import PdfReader, PdfWriter
    try:
        from PyPDF2 import PdfMerger  # 若版本支持
    except Exception:
        PdfMerger = None
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from PIL import Image
    import io
except ImportError as e:
    print(f"缺少必要的依赖包: {e}")
    print("请安装依赖包: pip install PyPDF2 reportlab Pillow")
    sys.exit(1)


def create_cover_page(cover_image_path, output_path):
    """
    创建封面页PDF
    
    Args:
        cover_image_path (str): 封面图片路径
        output_path (str): 输出PDF路径
    """
    # 创建PDF画布
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # A4尺寸 (595.27, 841.89) points
    page_width, page_height = A4
    
    try:
        # 打开图片并获取尺寸
        with Image.open(cover_image_path) as img:
            img_width, img_height = img.size
            
            # 计算缩放比例以适应A4页面
            scale_x = page_width / img_width
            scale_y = page_height / img_height
            scale = min(scale_x, scale_y)  # 保持宽高比
            
            # 计算居中位置
            new_width = img_width * scale
            new_height = img_height * scale
            x = (page_width - new_width) / 2
            y = (page_height - new_height) / 2
            
            # 绘制图片
            can.drawImage(cover_image_path, x, y, width=new_width, height=new_height)
            
    except Exception as e:
        print(f"处理封面图片时出错: {e}")
        # 如果图片处理失败，创建一个简单的文本封面
        can.setFont("Helvetica-Bold", 24)
        can.drawCentredText(page_width/2, page_height/2, "JumpServer 文档")
    
    can.save()
    
    # 将BytesIO内容写入PDF
    packet.seek(0)
    return PdfReader(packet)


def add_cover_to_pdf(original_pdf_path, cover_image_path, back_cover_image_path, output_pdf_path):
    """为 PDF 添加封面与封底 (可选)，保持书签与内部链接。

    Args:
        original_pdf_path (str): 原始PDF
        cover_image_path (str): 封面图片 (可为空或不存在则忽略)
        back_cover_image_path (str): 封底图片 (可为空或不存在则忽略)
        output_pdf_path (str): 输出PDF
    Returns:
        bool: True 成功 False 失败
    """
    try:
        if not os.path.exists(original_pdf_path):
            print(f"错误: 原始PDF不存在 -> {original_pdf_path}")
            return False

        print(f"原始PDF: {original_pdf_path}")
        print(f"封面: {cover_image_path if cover_image_path else '无'}")
        print(f"封底: {back_cover_image_path if back_cover_image_path else '无'}")

        # 优先使用 PdfMerger 以保留内部结构
        if PdfMerger is not None:
            try:
                print("模式: PdfMerger")
                merger = PdfMerger()

                # 封面
                if cover_image_path and os.path.exists(cover_image_path):
                    cover_reader = create_cover_page(cover_image_path, output_pdf_path)
                    import io as _io
                    buf_cover = _io.BytesIO()
                    w_cover = PdfWriter()
                    w_cover.add_page(cover_reader.pages[0])
                    w_cover.write(buf_cover)
                    buf_cover.seek(0)
                    merger.append(buf_cover)
                    print("已添加封面")
                elif cover_image_path:
                    print("封面文件不存在，忽略")

                # 原文档
                merger.append(original_pdf_path)

                # 封底
                if back_cover_image_path and os.path.exists(back_cover_image_path):
                    back_reader = create_cover_page(back_cover_image_path, output_pdf_path)
                    import io as _io
                    buf_back = _io.BytesIO()
                    w_back = PdfWriter()
                    w_back.add_page(back_reader.pages[0])
                    w_back.write(buf_back)
                    buf_back.seek(0)
                    merger.append(buf_back)
                    print("已添加封底")
                elif back_cover_image_path:
                    print("封底文件不存在，忽略")

                # 元数据
                try:
                    meta_reader = PdfReader(original_pdf_path)
                    if meta_reader.metadata:
                        merger.add_metadata({k: v for k, v in meta_reader.metadata.items() if isinstance(k, str)})
                except Exception:
                    pass

                with open(output_pdf_path, 'wb') as f_out:
                    merger.write(f_out)
                merger.close()
                print(f"输出: {output_pdf_path}")
                return True
            except Exception as e:
                print(f"PdfMerger 失败，回退: {e}")

        # 回退模式
        print("模式: 回退手动复制")
        reader = PdfReader(original_pdf_path)
        writer = PdfWriter()

        if cover_image_path and os.path.exists(cover_image_path):
            cover_pdf = create_cover_page(cover_image_path, output_pdf_path)
            writer.add_page(cover_pdf.pages[0])
            print("已添加封面 (回退)")

        for p in reader.pages:
            writer.add_page(p)

        if back_cover_image_path and os.path.exists(back_cover_image_path):
            back_pdf = create_cover_page(back_cover_image_path, output_pdf_path)
            writer.add_page(back_pdf.pages[0])
            print("已添加封底 (回退)")

        try:
            if reader.metadata:
                writer.add_metadata({k: v for k, v in reader.metadata.items() if isinstance(k, str)})
        except Exception:
            pass

        with open(output_pdf_path, 'wb') as f_out:
            writer.write(f_out)
        print(f"输出: {output_pdf_path}")
        return True
    except Exception as e:
        print(f"处理失败: {e}")
        return False


def main():
    """命令行入口"""
    import argparse
    script_dir = Path(__file__).parent.absolute()
    default_pdf = script_dir.parent / "site" / "pdf" / "document.pdf"
    default_cover = script_dir / "cover.jpg"
    default_out = script_dir / "document_with_cover.pdf"

    parser = argparse.ArgumentParser(description="为PDF添加封面/封底")
    parser.add_argument("--pdf", default=str(default_pdf), help="原始PDF路径")
    parser.add_argument("--cover", default=str(default_cover), help="封面图片路径(可选)")
    parser.add_argument("--back", default="", help="封底图片路径(可选)")
    parser.add_argument("--out", default=str(default_out), help="输出PDF路径")
    args = parser.parse_args()

    orig = Path(args.pdf)
    cover = Path(args.cover) if args.cover else None
    back = Path(args.back) if args.back else None
    out_path = Path(args.out)

    print("=" * 70)
    print("PDF 封面/封底 添加工具")
    print("=" * 70)
    print(f"原始PDF : {orig}")
    print(f"封面     : {cover if cover else '无'}")
    print(f"封底     : {back if back else '无'}")
    print(f"输出文件 : {out_path}")
    print("模式     : 优先 PdfMerger -> 回退 PageCopy")
    print("=" * 70)

    if orig.resolve() == out_path.resolve():
        print("错误: --out 不能与 --pdf 相同")
        return 2

    success = add_cover_to_pdf(str(orig), str(cover) if cover else "", str(back) if back else "", str(out_path))
    if success:
        print("\n✅ 完成")
        try:
            if orig.exists() and out_path.exists():
                s1 = os.path.getsize(orig)/1024/1024
                s2 = os.path.getsize(out_path)/1024/1024
                print(f"大小: {s1:.2f}MB -> {s2:.2f}MB")
        except Exception:
            pass
        return 0
    else:
        print("\n❌ 失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())

    success = add_cover_to_pdf(str(original_pdf), str(cover_image), str(back_cover_image) if back_cover_image else "", str(output_pdf))
