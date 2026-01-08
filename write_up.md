# write-up-task-1
## Kiến thức học được về fsop
- Đầu tiên thì em học được về cấu trúc của 1 file structure sẽ bao gồm các thành phần chính trong ảnh dưới đây
<img width="1723" height="839" alt="image" src="https://github.com/user-attachments/assets/9e422a4c-5be5-469a-a1ca-cf0c4846797c" />
- 1 số kiến thức cần chú ý là các loại ptr
- Mỗi loại ptr đều có 1 mục tiêu sử dụng riêng
- Và em có thể sử dụng chúng để thực hiện 1 trong 2 hành động là leak data hoặc ghi đè lên vùng mong muốn
### Read() to Arbitrary Memory
- Trước tiên thì hãy tìm hiểu cách để ghi đè lên 1 vùng mong muốn
- Để làm v thì em cần đáp ứng 1 vài điều kiện nhất định
<img width="1225" height="715" alt="image" src="https://github.com/user-attachments/assets/83de59bc-9ed0-478f-8662-bfd6ccb0e796" />
- Đối với các ptr thì chỉ cần thỏa các điều kiện này là đc, các ptr khác thì sao cũng được
- Bth để cho đẹp mắt thì có thể set về null nhưng nếu ko cần lắm thì em sẽ giữ nguyên như trong chall lần này
<img width="1781" height="689" alt="image" src="https://github.com/user-attachments/assets/3eb4e6a0-0717-4aef-a37d-8668ad4915cf" />
- Như ảnh ở trên thì cách phương pháp này hoạt động khá đơn giản, nhưng vì em mới học nên tốn khá nhiều thời gian làm quen
- 
