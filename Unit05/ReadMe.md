## **Unit04: 實作**

###抽詞任務：

在新聞報導的文本裡，有許多違法犯罪事件的新聞。其中，涉及諸如走私、廢棄物清理、政府採購法…等行為的犯罪人 ([參照：洗錢防制法](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0380131))，是會被列為需要特別注意的名單。

本單元的任務，就是設計並實作一個 NLP 模型，它可以產生的「特別注意名單」。

**語料說明：**

Corpus 中含有兩批資料，分別存放於 AML_News 和 Other_News 中。其中 AML_News 是「涉及違反洗錢防制法」的新聞，而 Other_News 則是「不涉及洗錢防制法」的新聞。

Test_News 中則是用來測試你的模型的新聞。裡面有一些是涉及違反洗錢防制法的新聞，有一些是不涉及洗錢防制法的新聞。

Gold.json 則是標準答案。 

```mermaid
graph TD;
    AML_News --> |Articut | VerbLIST_A;
    Other_News --> |Articut|  VerbLIST-B;
```